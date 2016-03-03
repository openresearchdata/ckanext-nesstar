# -*- coding: utf-8 -*-
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


class IgnoreDatasetError(Exception):
    pass

ignored_datasets = [
    'http://compass-data.unil.ch:80/obj/fStudy/COMPASS-SE-122014',
    'http://fors-getdata.unil.ch:80/obj/fStudy/ch.sidos.ddi.599.10890',
    'http://fors-getdata.unil.ch:80/obj/fStudy/ch.sidos.ddi.590.10890',
    'http://fors-getdata.unil.ch:80/obj/fStudy/ch.sidos.ddi.600.10890',
]


class NesstarHarvester(OaipmhHarvester):
    '''
    NESSTAR Harvester
    '''

    md_format = 'oai_ddi'

    def info(self):
        '''
        Return information about this harvester.
        '''
        return {
            'name': 'NESSTAR',
            'title': 'NESSTAR',
            'description': 'Harvester for NESSTAR data sources'
        }

    def _before_record_fetch(self, harvest_object):
        if (harvest_object.guid in ignored_datasets):
            log.debug('Ignore dataset %s' % harvest_object.guid)
            raise IgnoreDatasetError('Ignore dataset %s' % harvest_object.guid)

    def _extract_license_id(self, content):
        return 'FORS'

    def _get_possible_resource(self, harvest_obj, content):
        url = super(
            NesstarHarvester,
            self
        )._get_possible_resource(harvest_obj, content)
        if url:
            url = (
                'http://fors-getdata.unil.ch/webview/index.jsp?object=%s'
                % url
            )
        return url
