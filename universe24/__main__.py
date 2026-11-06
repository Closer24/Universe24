"""Generic reference runner. External observations never feed back into the state."""
import argparse
from contextlib import ExitStack
from dataclasses import asdict
import json
from pathlib import Path
import sys
from .experiments import checkpoint_data,load,read_checkpoint
from .observation import balance_residuals,clicks,expected_account_change,signed_account

def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Universe24 exact single-board engine")
    source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--config",type=Path,help="Data-only JSON seed")
    source.add_argument("--resume",type=Path,help="Full-state checkpoint")
    parser.add_argument("--steps",type=int)
    parser.add_argument("--events",type=Path,help="External arithmetic event log, JSONL")
    parser.add_argument("--output",type=Path,help="Final sparse full-state checkpoint")
    parser.add_argument("--audit",action="store_true",help="Inverse and signed-balance audits")
    args=parser.parse_args(argv)
    try:
        if args.config:
            experiment=load(args.config)
            engine,initial,count=experiment.engine,experiment.initial,0
            steps=experiment.steps if args.steps is None else args.steps
        else:
            if args.steps is None: parser.error("--steps is required with --resume")
            engine,initial,count=read_checkpoint(args.resume)
            steps=args.steps
        if type(steps) is not int or steps<0: parser.error("--steps must be nonnegative")
        targets=[p.resolve() for p in (args.events,args.output) if p is not None]
        inputs=[p.resolve() for p in (args.config,args.resume) if p is not None]
        if len(set(targets))!=len(targets) or any(p in inputs for p in targets):
            parser.error("Output paths must differ and not overwrite inputs")
        state=initial
        event_count=0
        with ExitStack() as stack:
            log=stack.enter_context(args.events.open("x",encoding="utf-8")) if args.events else None
            for index in range(1,steps+1):
                next_state=engine.advance(state)
                if args.audit:
                    if engine.rewind(next_state)!=state:
                        raise ArithmeticError("Inverse failed")
                    if balance_residuals(state,next_state,engine):
                        raise ArithmeticError("Local balance failed")
                    if signed_account(next_state)-signed_account(state)!=expected_account_change(state,engine):
                        raise ArithmeticError("Global signed-account identity failed")
                if log is not None:
                    for event in clicks(state,next_state,count+index):
                        log.write(json.dumps(asdict(event),separators=(",",":"))+"\n")
                        event_count+=1
                state=next_state
            if args.output:
                with args.output.open("x",encoding="utf-8") as handle:
                    json.dump(checkpoint_data(state,engine,count+steps),handle,indent=2)
                    handle.write("\n")
        print(json.dumps({"side":state.cube.side,"nodes":state.cube.node_count,
                          "channels_per_node":48,"completed_steps":count+steps,
                          "stored_deviations":len(state.cells),
                          "body_signs":engine.coupling.body_signs,
                          "coupling_fingerprint":engine.coupling.fingerprint,
                          "initial_signed_account":signed_account(initial),
                          "final_signed_account":signed_account(state),
                          "logged_arithmetic_events":event_count,"audited":args.audit},indent=2))
        return 0
    except (OSError,ValueError,TypeError,ArithmeticError) as error:
        print(f"Universe24: {error}",file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
