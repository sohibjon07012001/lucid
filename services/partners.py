from abc import *
import typing

from db.users import User, Partner, Engineer, EngineerPartner
import exceptions


from services.facade import AbsPartnerService


class PartnerService_Engineer(AbsPartnerService):    
    async def get_partners(self) -> typing.List[Partner]:
        """Returns partners which the engineer bind to"""
        related_matrix = await EngineerPartner.filter(engineer=self.services.user.engineer_profile).prefetch_related('partner', 'engineer')
        return [i.partner for i in related_matrix]


class PartnerService_Partner(AbsPartnerService):
    async def get_partners(self) -> typing.List[Partner]:
        """Partner is not allowed to see other partners"""
        raise exceptions.FORBIDDEN


class PartnerService_Admin(AbsPartnerService):
    async def get_partners(self) -> typing.List[Partner]:
        """Admin can see all the partners registered in Database"""
        return [p for p in await Partner.filter()]