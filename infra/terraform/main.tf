###############################################################################
#  Terraform — Software3-Lab (EKS + Helm)
###############################################################################

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws        = { source = "hashicorp/aws",  version = "~> 5.47" }
    helm       = { source = "hashicorp/helm", version = "~> 2.13" }
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.29" }
  }
}

###############################################################################
#  1. AWS Provider
###############################################################################
provider "aws" {
  region = var.aws_region
}

###############################################################################
#  2. EKS Cluster (terraform-aws-modules)  ─── comment out if using existing
###############################################################################
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.13.0"

  cluster_name    = "software3-lab-eks"
  cluster_version = "1.29"

  vpc_id     = var.vpc_id
  subnet_ids = var.public_subnet_ids

  eks_managed_node_groups = {
    default = {
      instance_types   = ["t3.large"]
      desired_capacity = 2
      min_capacity     = 1
      max_capacity     = 3
    }
  }
}

###############################################################################
#  3. Helm Provider (uses EKS kubeconfig from module)
###############################################################################
provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    token                  = module.eks.cluster_token
  }
}

###############################################################################
#  4. Helm Release — deploy Software3-Lab
###############################################################################
resource "helm_release" "software3_lab" {
  name       = "software3-lab"
  chart      = "${path.module}/../helm/software3-lab"
  namespace  = "software3"
  create_namespace = true

  # Optional: override defaults
  set {
    name  = "image.repository"
    value = "trojan3877/software3-lab"
  }
  set {
    name  = "image.tag"
    value = "0.1.0"
  }
}

###############################################################################
#  5. Outputs
###############################################################################
output "cluster_name" {
  value = module.eks.cluster_name
}

output "kubeconfig" {
  value     = module.eks.kubeconfig
  sensitive = true
}

###############################################################################
#  6. Variables
###############################################################################
variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "Existing VPC ID"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}
