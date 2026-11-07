"""Finalize recorded PNG sequences as serial, decoded, immutable GIF files.

ffmpeg writes only to a captured pipe. Python waits for it to exit, decodes
the complete bytes, then creates a new content-addressed output file. No
encoder ever opens a delivery pathname, and no scientific state is altered.
"""
import argparse
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import time

from PIL import Image


def sha(raw):return hashlib.sha256(raw).hexdigest()


def decoded(raw,expected):
    if not raw:raise ValueError('Encoded animation is empty')
    with Image.open(BytesIO(raw))as im:
        if im.format!='GIF'or im.n_frames!=expected:raise ValueError('Wrong animation format/frame count')
        size=im.size;durations=[]
        for i in range(im.n_frames):
            im.seek(i);im.load();durations.append(im.info.get('duration'))
    if size!=(800,450)or any(v!=250 for v in durations):
        raise ValueError('Unexpected animation geometry or recorded-frame duration')
    return {'format':'GIF','frames':expected,'size':list(size),'frame_duration_ms':250,'all_frames_decoded':True}


def finalize(input_dir,output_dir,html_path):
    input_dir=Path(input_dir).resolve();output_dir=Path(output_dir).resolve();html_path=Path(html_path).resolve()
    original_raw=(input_dir/'report.json').read_bytes();original=json.loads(original_raw)
    if not original['passed']or original['verification_mode']!='animation_only':raise ValueError('Expected completed animation capture')
    if sha(html_path.read_bytes())!=original['input_sha256']:raise ValueError('HTML identity mismatch')
    for entry in original['images']:
        path=(input_dir/entry['file']).resolve()
        if not path.is_relative_to(input_dir)or sha(path.read_bytes())!=entry['sha256']:
            raise ValueError('Recorded source PNG changed')
    output_dir.mkdir(parents=True,exist_ok=False);start=time.monotonic();records=[]
    report={'format':'universe24-verified-animation-delivery-v1','passed':False,
        'source_capture_report':str(input_dir/'report.json'),'source_capture_report_sha256':sha(original_raw),
        'html_path':str(html_path),'html_sha256':original['input_sha256'],
        'converter_source_sha256':sha(Path(__file__).read_bytes()),
        'scientific_states_changed':False,'encoder_opens_delivery_paths':False,
        'scope':'Serial GIF encoding from hash-verified actual Presenter PNGs; no browser CSS or native-pointer validation.',
        'animations':records}
    try:
        for index,sequence in enumerate(original['sequences'],1):
            if time.monotonic()-start>240:raise TimeoutError('Animation finalization wall budget exhausted')
            frames=sequence['last_frame']-sequence['first_frame']+1
            folder=input_dir/f'sequence-{index:02d}'
            args=['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-filter_threads','1',
                  '-framerate','4','-i',str(folder/'frame-%03d.png'),'-filter_complex',
                  'scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3',
                  '-loop','0','-f','gif','pipe:1']
            completed=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=60)
            raw=completed.stdout;decode=decoded(raw,frames);digest=sha(raw)
            name=f'{sequence["experiment"]}-{digest[:16]}.gif';target=output_dir/name
            with target.open('xb')as handle:
                handle.write(raw);handle.flush();os.fsync(handle.fileno())
            if target.read_bytes()!=raw:raise ValueError('Delivery bytes differ after close')
            records.append({'experiment':sequence['experiment'],'file':name,'sha256':digest,'bytes':len(raw),
                'first_frame':sequence['first_frame'],'last_frame':sequence['last_frame'],
                'decode':decode,'encoder_exit_code':completed.returncode,'command':args,
                'source_png_sha256':{e['file']:e['sha256']for e in original['images']if e['file'].startswith(f'sequence-{index:02d}/frame-')}})
        # All encoder subprocesses have exited; re-read and fully decode every
        # delivery file once more, rather than trusting earlier memory bytes.
        for record in records:
            raw=(output_dir/record['file']).read_bytes()
            if sha(raw)!=record['sha256']:raise ValueError('Final animation changed after encoder exit')
            decoded(raw,record['decode']['frames'])
        report['all_writers_exited']=True;report['final_file_reads_and_decodes_passed']=True;report['passed']=True
    except Exception as exc:
        report['failure']={'type':type(exc).__name__,'message':str(exc)};raise
    finally:
        report['wall_seconds']=time.monotonic()-start
        with(output_dir/'report.json').open('x')as handle:json.dump(report,handle,indent=2)
    print(json.dumps({'passed':True,'animations':len(records),'wall_seconds':report['wall_seconds']}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--html',type=Path,required=True);args=parser.parse_args()
    finalize(args.input,args.output,args.html)
