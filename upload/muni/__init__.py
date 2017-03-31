from ashdod import AshdodMuni
from beer_sheva import BeerMuni
from gush_etzion import GushMuni
from hura import HuraMuni
from kfar_shmaryahu import KfarShmaryahuMuni
from qiryat_bialik import QiryatBialikMuni
from rehovot import RehovotMuni
from rishon_letzion import RishonLetzionMuni
from tel_aviv import TelAvivMuni
from jerusalem import JerusalemMuni
from kfar_saba import KfarSabaMuni
from netanya import NetanyaMuni
from petah_tikva import PetahTikvaMuni
from givatayim import GivatayimMuni
from omer import OmerMuni
from hadera import HaderaMuni
from haifa import HaifaMuni
from hertzelia import HertzeliaMuni
from holon import HolonMuni
from ramat_gan import RamatGanMuni
from schema import SchemaMuni

# Might need a FIXME: if we override one of the keys...
munis_loaders = {AshdodMuni.MUNI:AshdodMuni,
                 BeerMuni.MUNI: BeerMuni,
                 GushMuni.MUNI: GushMuni,
                 HuraMuni.MUNI: HuraMuni,
                 KfarShmaryahuMuni.MUNI: KfarShmaryahuMuni,
                 QiryatBialikMuni.MUNI: QiryatBialikMuni,
                 RehovotMuni.MUNI: RehovotMuni,
                 RishonLetzionMuni.MUNI: RishonLetzionMuni,
                 TelAvivMuni.MUNI: TelAvivMuni,
                 JerusalemMuni.MUNI: JerusalemMuni,
                 KfarSabaMuni.MUNI: KfarSabaMuni,
                 NetanyaMuni.MUNI: NetanyaMuni,
                 PetahTikvaMuni.MUNI: PetahTikvaMuni,
                 GivatayimMuni.MUNI: GivatayimMuni,
                 OmerMuni.MUNI: OmerMuni,
                 HaderaMuni.MUNI: HaderaMuni,
                 HertzeliaMuni.MUNI: HertzeliaMuni,
                 HaifaMuni.MUNI: HaifaMuni,
                 HolonMuni.MUNI: HolonMuni,
                 RamatGanMuni.MUNI: RamatGanMuni,
                 }
