# Build  backend
cd backend
docker build  -t  coderpews/jenkins-plugins-scanner-backend  .

# Build  frontend
cd frontend
docker build  -t  coderpews/jenkins-plugins-scanner-frontend  .

## local cluster
kind create cluster

## istio
```
istioctl operator init

kubectl create ns istio-system

kubectl apply -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
  name: example-istiocontrolplane
spec:
  profile: demo
EOF
```

# Rollout
```
kubectl apply -f ns.yaml
kubectl apply -f  gateway.yaml
kubectl apply -f deploy.yaml
```