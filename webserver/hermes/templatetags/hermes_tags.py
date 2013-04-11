from django import template
from competition.models.game_model import Game

import slumber
import logging

logger = logging.getLogger(__name__)

register = template.Library()


class CheckEmbargoedNode(template.Node):
    def __init__(self, team, variable_name):
        self.team = team
        self.variable_name = variable_name

    def render(self, context):
        team = context[self.team]
        try:
            # Get the last game played
            last_game = team.game_set.latest()

            # Grag the API url from the last Game that was played
            url = last_game.data['api_url']

            # Query API
            response = slumber.API(url).client.get(name=team.name)

            # Make sure that we only get one client item back.
            assert response['meta']['total_count'] == 1

            # Get "embargoed" from returned client
            if response['objects'][0]['embargoed']:
                result = "embargoed"
            else:
                result = "unembargoed"
        except Game.DoesNotExist:
            result = "not ready"
        except KeyError:
            result = "error"
        except AssertionError:
            result = "error"
            msg = "Found more than one team with name {} in arena"
            logger.error(msg.format(team.name))

        context[self.variable_name] = result
        return ""


@register.tag
def check_embargoed(parser, token):
    try:
        tag_name, team, _as, variable = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        msg = '{0} should be "{0} <team> as <variable>"'
        raise template.TemplateSyntaxError(msg.format(tag_name))
    return CheckEmbargoedNode(team, variable)