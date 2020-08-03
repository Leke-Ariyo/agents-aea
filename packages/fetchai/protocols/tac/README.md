# TAC Protocol

**Name:** tac

**Author**: fetchai

**Version**: 0.4.0

**Short Description**: The tac protocol implements the messages an AEA needs to participate in a Trading Agent Competition (TAC).

**License**: Apache-2.0

## Description

This is a protocol for participating in a Trading Agent Competition (TAC). 

## Specification

```yaml
---
name: tac
author: fetchai
version: 0.4.0
description: The tac protocol implements the messages an AEA needs to participate
  in the TAC.
license: Apache-2.0
aea_version: '>=0.5.0, <0.6.0'
speech_acts:
  register:
    agent_name: pt:str
  unregister: {}
  transaction:
    transaction_id: pt:str
    ledger_id: pt:str
    sender_address: pt:str
    counterparty_address: pt:str
    amount_by_currency_id: pt:dict[pt:str, pt:int]
    fee_by_currency_id: pt:dict[pt:str, pt:int]
    quantities_by_good_id: pt:dict[pt:str, pt:int]
    nonce: pt:str
    sender_signature: pt:str
    counterparty_signature: pt:str
  cancelled: {}
  game_data:
    amount_by_currency_id: pt:dict[pt:str, pt:int]
    exchange_params_by_currency_id: pt:dict[pt:str, pt:float]
    quantities_by_good_id: pt:dict[pt:str, pt:int]
    utility_params_by_good_id: pt:dict[pt:str, pt:float]
    fee_by_currency_id: pt:dict[pt:str, pt:int]
    agent_addr_to_name: pt:dict[pt:str, pt:str]
    currency_id_to_name: pt:dict[pt:str, pt:str]
    good_id_to_name: pt:dict[pt:str, pt:str]
    version_id: pt:str
    info: pt:optional[pt:dict[pt:str, pt:str]]
  transaction_confirmation:
    transaction_id: pt:str
    amount_by_currency_id: pt:dict[pt:str, pt:int]
    quantities_by_good_id: pt:dict[pt:str, pt:int]
  tac_error:
    error_code: ct:ErrorCode
    info: pt:optional[pt:dict[pt:str, pt:str]]
...
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
    GENERIC_ERROR = 0;
    REQUEST_NOT_VALID = 1;
    AGENT_ADDR_ALREADY_REGISTERED = 2;
    AGENT_NAME_ALREADY_REGISTERED = 3;
    AGENT_NOT_REGISTERED = 4;
    TRANSACTION_NOT_VALID = 5;
    TRANSACTION_NOT_MATCHING = 6;
    AGENT_NAME_NOT_IN_WHITELIST = 7;
    COMPETITION_NOT_RUNNING = 8;
    DIALOGUE_INCONSISTENT = 9;
  }
  ErrorCodeEnum error_code = 1;
...
---
initiation: [register]
reply:
  register: [tac_error, game_data, cancelled]
  unregister: [tac_error]
  transaction: [transaction_confirmation,tac_error]
  cancelled: []
  game_data: [transaction]
  transaction_confirmation: [transaction]
  tac_error: []
termination: [cancelled, tac_error]
roles: {participant, controller}
end_states: [successful, failed]
...
```

## Links

* <a href="https://docs.fetch.ai/aea/tac-skills/" target=_blank>TAC skill in the AEA framework</a>