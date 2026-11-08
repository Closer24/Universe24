"""The ONLY forward state-changing primitive. num=den=1; divisor=6."""
from .state import Channel

def forward(old:Channel,neighbor_sum:int)->Channel:
    ell,remainder=divmod(2*neighbor_sum+old.r,6)
    return Channel(old.b,ell-old.a,remainder)

def inverse(new:Channel,old_neighbor_sum:int)->Channel:
    k=2*old_neighbor_sum
    remainder=(new.r-k)%6
    old_a=(k+remainder-new.r)//6-new.b
    return Channel(old_a,new.a,remainder)
