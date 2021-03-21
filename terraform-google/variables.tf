variable "gce_ssh_user" {
  default = "gcp_user"
}

variable "gce_ssh_pub_key_file" {
  default = "../secrets/gcp_key.pub"
}

variable "gce_ssh_private_key_file" {
  default = "../secrets/gcp_key"
}