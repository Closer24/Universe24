"""Retired amplitude-matched router calibration.

At divisor six the required 16*kappa*A*A = 6 has no positive integer
solution. An arbitrary polynomial detector is still available in choice.py,
but it is not a matched Born router.
"""
def near_matched_kappa(A=1):
    raise NotImplementedError("16*kappa*A*A = 6 has no positive integer solution")
def predicted_non_detection(A=1):
    raise NotImplementedError("the matched-router calibration was removed")
def build_odd_q_router(*, A, arm1, arm2, form="opposite", name="router"):
    raise NotImplementedError("the matched-router calibration was removed")
