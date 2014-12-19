from ckanext.oaipmh.harvester import OaipmhHarvester
import logging


log = logging.getLogger(__name__)


class NesstarHarvester(OaipmhHarvester):
    '''
    NESSTAR Harvester
    '''

    def info(self):
        '''
        Return information about this harvester.
        '''
        return {
            'name': 'NESSTAR',
            'title': 'NESSTAR',
            'description': 'Harvester for NESSTAR data sources'
        }
