from invoke import task
from os import system

MINIKUBE="/usr/bin/env minikube"
KUSTOMIZE="/usr/bin/env kustomize"
KUBECTL="/usr/bin/env kubectl"

def start_minicube(MINIKUBE):
	system( MINIKUBE + """ start \
	--kubernetes-version=v1.23.3 \
	--driver=virtualbox \
	--cpus=6 \
	--memory=8g \
	--bootstrapper=kubeadm \
	--extra-config=kubelet.authentication-token-webhook=true \
	--extra-config=kubelet.authorization-mode=Webhook \
	--extra-config=scheduler.address=0.0.0.0 \
	--extra-config=controller-manager.address=0.0.0.0
	minikube config unset vm-driver
	minikube addons enable ingress
	minikube addons enable default-storageclass
	minikube addons enable storage-provisioner
	minikube addons enable metrics-server""")

@task
def minikube(c):
    start_minicube(MINIKUBE)

@task
def deploy(c):
    start_minicube(MINIKUBE)
    c.run(KUSTOMIZE + " build ./overlays/dev | kubectl apply -f -")

@task
def destroy(c):
    c.run(MINIKUBE + " delete")

@task
def get_pods(c):
    c.run(KUBECTL + " get pods")