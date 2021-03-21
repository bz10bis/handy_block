terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file("../secrets/blockchain-monitoring-solution.json")

  project = "blockchain-monitoring-solution"
  region = "us-central1"
  zone = "us-central1-c"
}

//resource "google_compute_network" "vpc_network" {
//  name = "corda-network"
//}

resource "random_string" "bucket" {
  length = 8
  special = false
  upper = false
}

resource "google_storage_bucket" "corda_share" {
  name = "corda-vault-${random_string.bucket.result}"
  location = "US"
}

resource "google_compute_instance" "corda_nodes" {
  depends_on = [google_storage_bucket.corda_share]
  count = 3

  name = "corda-node-${count.index}"
  machine_type = "f1-micro"

  boot_disk {
    initialize_params {
      image = "centos-7"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-key = "${var.gce_ssh_user}:${file(var.gce_ssh_pub_key_file)}"
  }

  provisioner "remote-exec" {
    // inline = ["sudo yum update -y", "sudo yum install python3 -y", "echo Done!"]
    inline = ["sudo yum install python3 -y", "echo Done!"]

    connection {
      host        = self.network_interface.0.access_config.0.nat_ip
      type        = "ssh"
      user        = "gcp_user"
      timeout     = "2m"
      private_key = file(var.gce_ssh_private_key_file)
    }
  }

  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u root -i '${self.network_interface.0.access_config.0.nat_ip},' --private-key ${var.gce_ssh_private_key_file} -e 'pub_key=${var.gce_ssh_pub_key_file}' -i ../ansible-corda/inventories/corda-inventory ../ansible-corda/main.yml"
  }
}
