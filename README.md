# Parkside PRMA 20-li Home Assistant integration

Taken from those repositories

https://github.com/Whytey/pymoebot
https://github.com/Whytey/moebot-hass-integration

and tweaked to support most of the Parkside PRMA 20-li functions

## Example notification
```
alias: Kosiarka - error
description: ""
triggers:
  - trigger: state
    entity_id:
      - sensor.kosiarka_ostrzezenie
    from:
      - NONE
  - trigger: numeric_state
    entity_id:
      - sensor.kosiarka_blad
    attribute: errorCount
    above: 0
  - trigger: state
    entity_id:
      - sensor.kosiarka_stan_kosiarki
    to:
      - EMERGENCY
conditions: []
actions:
  - variables:
      lista_bledow: >
        {% set ns = namespace(errors=[]) %}  
        {% if states('sensor.kosiarka_ostrzezenie') != 'NONE'%}
          {% set ns.errors = ns.errors + [ state_translated('sensor.kosiarka_ostrzezenie') ] %}
        {% endif %}
        
        {% if states('sensor.kosiarka_stan_kosiarki') == 'EMERGENCY'%}
          {% set ns.errors = ns.errors + [ state_translated('sensor.kosiarka_stan_kosiarki') ] %}
        {% endif %}

        {% if state_attr('sensor.kosiarka_blad', 'errorCount') > 0 %}
          {% for attr in states.sensor.kosiarka_blad.attributes if attr.startswith('ERROR_') %}
            {% set ns.errors = ns.errors + [ state_attr_translated('sensor.kosiarka_blad', attr) ] %}
          {% endfor %}
        {% endif %}

        {{ns.errors | join(', ') if ns.errors | count > 0 else '' }}
  - condition: template
    value_template: "{{ lista_bledow | length > 0 }}"
  - action: notify.mobile_app_xxxx
    metadata: {}
    data:
      message: "{{lista_bledow}}"
      title: Kosiarka
      data:
        color: green
        channel: Urzadzenia
        importance: high
        ttl: 0
        priority: high
        notification_icon: mdi:mower-bag-on
    enabled: true
```
