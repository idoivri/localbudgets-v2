from ashdod import AshdodMuni
from beer_sheva import BeerMuni
from gush_etzion import GushMuni
from hura import HuraMuni
from kfar_shmaryahu import KfarShmaryahuMuni
from qiryat_bialik import QiryatBialikMuni
from rehovot import RehovotMuni
from rishon_letzion import RishonLetzionMuni
from schema import SchemaMuni

# Might need a FIXME: if we override one of the keys...
munis_loaders = {AshdodMuni.MUNI :AshdodMuni,
                 BeerMuni.MUNI : BeerMuni,
                 GushMuni.MUNI : GushMuni,
                 HuraMuni.MUNI : HuraMuni,
                 KfarShmaryahuMuni.MUNI : KfarShmaryahuMuni,
                 QiryatBialikMuni.MUNI : QiryatBialikMuni,
                 RehovotMuni.MUNI : RehovotMuni,
                 RishonLetzionMuni.MUNI : RishonLetzionMuni,
                 SchemaMuni.MUNI : SchemaMuni


                 }