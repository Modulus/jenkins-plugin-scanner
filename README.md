# Build  frontend
cd frontend
npm run build

# Build  backend
cp -r dist ../backend
cd ../backend
docker build  -t  coderpews/jenkins-plugins-scanner  .

# Note after update
The frontend is copied and hosted from the backend at this moment.

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

Triggerring commit hook!
