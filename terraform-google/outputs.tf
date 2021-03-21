resource "local_file" "AnsibleInventory" {
  content = templatefile("inventory.tmpl",
  {
    corda-name = google_compute_instance.corda_nodes.*.name,
    corda-ip = google_compute_instance.corda_nodes.*.network_interface.0.access_config.0.nat_ip,
    corda-id = google_compute_instance.corda_nodes.*.id
  }
  )
  filename = "../ansible-corda/inventories/corda-inventory"
}