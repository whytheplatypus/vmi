provider "aws" {
  region = "us-west-1"
}

##############################################################
# Data sources to get VPC, subnets and security group details
##############################################################
data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = "${data.aws_vpc.default.id}"
}

data "aws_security_group" "default" {
  vpc_id = "${data.aws_vpc.default.id}"
  name   = "default"
}

variable "environment" {
  type    = "string"
}

variable "dbname" {
  type    = "string"
  default = "devdb"
}

variable "db_size" {
  type    = "string"
  default = "db.t2.micro"
}

variable "db_username" {
  type = "string"
}

resource "random_string" "db_password" {
  length = 16
  special = true
  override_special = "/@\" "
}

#####
# DB
#####
module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "${var.dbname}"

  engine            = "postgres"
  engine_version    = "9.6.3"
  instance_class    = "${var.db_size}"
  allocated_storage = 5
  storage_encrypted = false

  # kms_key_id        = "arm:aws:kms:<region>:<account id>:key/<kms key id>"

  name = "${var.dbname}"
  # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
  # "Error creating DB Instance: InvalidParameterValue: MasterUsername
  # user cannot be used as it is a reserved word used by the engine"
  username = "${var.db_username}"
  password = "${random_string.db_password.result}"
  port     = "5432"
  vpc_security_group_ids = ["${data.aws_security_group.default.id}"]
  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"
  # disable backups to create DB faster
  backup_retention_period = 0
  tags = {
    Owner       = "user"
    Environment = "dev"
  }
  # DB subnet group
  subnet_ids = ["${data.aws_subnet_ids.all.ids}"]
  # DB parameter group
  family = "postgres9.6"
  # DB option group
  major_engine_version = "9.6"
  # Snapshot name upon DB deletion
  final_snapshot_identifier = "${var.dbname}"
}

resource "aws_ssm_parameter" "db_password" {
  name  = "/${var.environment}/database/password/${var.db_username}"
  description  = "Database password"
  type  = "SecureString"
  value = "${random_string.db_password.result}"

  tags {
    environment = "${var.environment}"
  }
}
