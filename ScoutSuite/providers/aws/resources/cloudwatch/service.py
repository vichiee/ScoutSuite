from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.resources import AWSResources

from ScoutSuite.providers.utils import get_non_provider_id


class Alarms(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_alarms = self.facade.cloudwatch.get_alarms(self.scope['region'])
        for raw_alarm in raw_alarms:
            name, resource = self._parse(raw_alarm)
            self[name] = resource

    def _parse(self, raw_alarm):
        """
        Parse a single CloudWatch trail

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param alarm:                   Alarm
        """

        raw_alarm['arn'] = raw_alarm.pop('AlarmArn')
        raw_alarm['name'] = raw_alarm.pop('AlarmName')
        
        # Drop some data
        for k in ['AlarmConfigurationUpdatedTimestamp', 'StateReason', 'StateReasonData', 'StateUpdatedTimestamp']:
            if k in raw_alarm:
                raw_alarm.pop(k)

        alarm_id = get_non_provider_id(raw_alarm['arn'])
        return alarm_id, raw_alarm


class CloudWatch(Regions):
    _children = [
        (Alarms, 'alarms')
    ]

    def __init__(self):
        super(CloudWatch, self).__init__('cloudwatch')
