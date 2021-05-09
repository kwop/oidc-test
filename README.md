# STARTER KIT

## TEST LOCALLY

Prerequisite

- bash
- make
- docker
- docker-compose
- Create a OIDC application with OKTA.


Spin up the project

Show available commands

```
make 
```



Next :

```
mv oidc-front/client_secrets.json.dist oidc-front/client_secrets.json
make start
```

Next :

Go to http://localhost:8080/

If you want to modify the project code : 

go to folder oidc-front/main.py, flask will auto reload on code change.

## PUBLISH ON KUBERNETES

Prerequisites

- bash
- make
- nginx-ingress-controller > v0.9.0 
- kubernetes
- helm 3
- helmfile

###### from helmfile

```
make install-helmfile
```

to uninstall 

```
make uninstall-helmfile
```

###### from helm charts

```
make install-okta-firewall
make install-okta-protected-endpoint
```

(optionnal)
Add hosts in /etc/hosts
```
<CLUSTER IP> user1337-okta-protected-endpoint.xip.io
<CLUSTER IP> user33-okta-protected-endpoint.xip.io
<CLUSTER IP> okta-firewall.xip.io
```

Go to https://user1337-okta-protected-endpoint.xip.io

## Troubleshooting

Ingress controller error log (rke cluster)

( Adjust the namespace for your cluster spec )

```
kubectl get pod -n ingress-nginx
kubectl logs pod/<POD NAME> -n ingress-nginx
```

OIDC url troobleshoot

Go to https://okta-firewall.xip.io


DNS ingress fix 

See ingress annotation ( and change resolver ) : 

    nginx.ingress.kubernetes.io/auth-snippet: |
      resolver 127.0.0.53 valid=15s;

Play with the k8s/k3s node hosts...
