#
# Copyright 2023 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import json
import logging
import time
from _decimal import Decimal
from datetime import datetime, timezone
from hashlib import sha256
import os

import requests

from aquarius.app.util import get_aquarius_wallet, get_signature_bytes
from aquarius.events.util import update_did_state

logger = logging.getLogger(__name__)
# default will notspend more that 4 seconds.. if it fails, we will retry it
event_request_timeout = int(os.environ.get("EVENTS_REQUEST_TIMEOUT", 4))


def decrypt_ddo(w3, provider_url, contract_address, chain_id, txid, hash, es_instance):
    aquarius_account = get_aquarius_wallet()
    nonce = Decimal(time.time_ns())

    signature = get_signature_bytes(
        f"{txid}{aquarius_account.address}{chain_id}{str(nonce)}"
    )
    payload = {
        "transactionId": txid,
        "chainId": chain_id,
        "decrypterAddress": aquarius_account.address,
        "dataNftAddress": contract_address,
        "signature": signature,
        "nonce": str(nonce),
    }

    try:
        response = requests.post(
            provider_url + "/api/services/decrypt", timeout=event_request_timeout, json=payload
        )
    except Exception as e:
        response = None

    if not hasattr(response, "status_code"):
        msg = f"Failed to get a response for decrypt DDO with provider={provider_url}, payload={payload}, response={response}"
        update_did_state(es_instance, contract_address, chain_id, txid, False, msg)
        logger.error(msg)
        raise Exception(f"in decrypt_ddo: {msg}")

    if response.status_code == 201:
        if sha256(response.content).hexdigest() != hash.hex():
            msg = f"Hash check failed: response={response.content}, encoded response={sha256(response.content).hexdigest()}\n metadata hash={hash.hex()}"
            logger.error(msg)
            update_did_state(es_instance, contract_address, chain_id, txid, False, msg)
            raise Exception(f"in decrypt_ddo: {msg}")
        logger.info("Decrypted DDO successfully.")
        response_content = response.content.decode("utf-8")
        return json.loads(response_content)

    if response.status_code == 403:
        # unauthorised decrypter
        msg = f"403, response={response.content}"
        update_did_state(es_instance, contract_address, chain_id, txid, False, msg)
        logger.info(msg)
        return False

    msg = f"Provider exception on decrypt DDO. Status:{response.status_code},  {response.content}\n provider URL={provider_url}, payload={payload}."
    update_did_state(es_instance, contract_address, chain_id, txid, False, msg)
    logger.error(msg)
    raise Exception(f"in decrypt_ddo: {msg}")
