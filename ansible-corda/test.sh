ANSIBLE_HOST_KEY_CHECKING=False ansible -u gcp_user -i ./inventories/corda-inventory --private-key ../secrets/gcp_key -e 'pub_key=../secret/gcp_key.pub' -m ping corda