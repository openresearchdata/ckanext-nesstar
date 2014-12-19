from ckanext.oaipmh.harvester import OaipmhHarvester
import oaipmh
import datetime
import logging
from oaipmh.error import DatestampError

log = logging.getLogger(__name__)

orginal_datestamp_to_datetime = oaipmh.datestamp._datestamp_to_datetime


# monkey-patch pyoai to handle wrong date formats
def datestamp_to_datetime_for_wrong_input(datestamp, inclusive=False):
    try:
        return orginal_datestamp_to_datetime(datestamp, inclusive)
    except oaipmh.error.DatestampError:
        try:
            return oaipmh.datestamp.tolerant_datestamp_to_datetime(datestamp)
        except oaipmh.error.DatestampError:
            pass

    splitted = datestamp.split('T')
    if len(splitted) == 2:
        d, t = splitted
        if not t:
            raise DatestampError(datestamp)
        if t[-1] == 'Z':
            t = t[:-1]  # strip off 'Z'
        t = t.split('+')[0]  # remove timezone info
    else:
        d = splitted[0]
        if inclusive:
            # used when a date was specified as ?until parameter
            t = '23:59:59'
        else:
            t = '00:00:00'
    YYYY, MM, DD = d.split('-')
    hh, mm, ss = t.split(':')  # this assumes there's no timezone info
    return datetime.datetime(
        int(YYYY),
        int(MM),
        int(DD),
        int(hh),
        int(mm),
        int(ss)
    )

oaipmh.datestamp._datestamp_to_datetime = datestamp_to_datetime_for_wrong_input
oaipmh.client.datestamp_to_datetime = datestamp_to_datetime_for_wrong_input





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
