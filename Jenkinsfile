pipeline {
    agent none
    environment {
        GIT_REPO_SLUG = "Dullage/gunicorn-python"
        DOCKER_REPO_SLUG = "Dullage/gunicorn-python"
        DOCKER_CREDENTIALS = credentials('docker')
        DOCKER_CLI_EXPERIMENTAL = "enabled"
    }
    stages {
        stage("Build") {
            parallel {
                stage("Build (amd64)") {
                    agent { label "docker && amd64" }
                    steps {
                        // 3.8
                        sh "docker build -t $DOCKER_REPO_SLUG:3.8-amd64 $WORKSPACE/3.8"
                        sh "docker save -o 3.8-amd64.tar $DOCKER_REPO_SLUG:3.8-amd64"
                        // 3.8-alpine
                        sh "docker build -t $DOCKER_REPO_SLUG:3.8-alpine-amd64 $WORKSPACE/3.8-alpine"
                        sh "docker save -o 3.8-alpine-amd64.tar $DOCKER_REPO_SLUG:3.8-alpine-amd64"
                        // Stash
                        stash includes: "*.tar", name: "amd64"
                    }
                }
                stage("Build (arm32v7)") {
                    agent { label "docker && arm32v7" }
                    steps {
                        // 3.8
                        sh "docker build -t $DOCKER_REPO_SLUG:3.8-arm32v7 $WORKSPACE/3.8"
                        sh "docker save -o 3.8-arm32v7.tar $DOCKER_REPO_SLUG:3.8-arm32v7"
                        // 3.8-alpine
                        sh "docker build -t $DOCKER_REPO_SLUG:3.8-alpine-arm32v7 $WORKSPACE/3.8-alpine"
                        sh "docker save -o 3.8-alpine-arm32v7.tar $DOCKER_REPO_SLUG:3.8-alpine-arm32v7"
                        // Stash
                        stash includes: "*.tar", name: "arm32v7"
                    }
                }
            }
        }
        stage("Deploy Builds") {
            when { branch "master" }
            parallel {
                stage("Deploy (amd64)") {
                    agent { label "docker && amd64" }
                    steps {
                        unstash "amd64"
                        sh "echo '$DOCKER_CREDENTIALS_PSW' | docker login -u '$DOCKER_CREDENTIALS_USR' --password-stdin"
                        // 3.8
                        sh "docker load -i 3.8-amd64.tar"
                        sh "docker push $DOCKER_REPO_SLUG:3.8-amd64"
                        // 3.8-alpine
                        sh "docker load -i 3.8-alpine-amd64.tar"
                        sh "docker push $DOCKER_REPO_SLUG:3.8-alpine-amd64"
                    }
                }
                stage("Deploy (arm32v7)") {
                    agent { label "docker && arm32v7" }
                    steps {
                        unstash "arm32v7"
                        sh "echo '$DOCKER_CREDENTIALS_PSW' | docker login -u '$DOCKER_CREDENTIALS_USR' --password-stdin"
                        // 3.8
                        sh "docker load -i 3.8-arm32v7.tar"
                        sh "docker push $DOCKER_REPO_SLUG:3.8-arm32v7"
                        // 3.8-alpine
                        sh "docker load -i 3.8-alpine-arm32v7.tar"
                        sh "docker push $DOCKER_REPO_SLUG:3.8-alpine-arm32v7"
                    }
                }
            }
        }
        stage("Create & Deploy Manifests") {
            when { branch "master" }
            agent { label "docker" }
            steps {
                sh "echo '$DOCKER_CREDENTIALS_PSW' | docker login -u '$DOCKER_CREDENTIALS_USR' --password-stdin"
                // 3.8
                sh "docker manifest create $DOCKER_REPO_SLUG:3.8 $DOCKER_REPO_SLUG:3.8-amd64 $DOCKER_REPO_SLUG:3.8-arm32v7"
                sh "docker manifest push $DOCKER_REPO_SLUG:3.8"
                // 3.8-alpine
                sh "docker manifest create $DOCKER_REPO_SLUG:3.8-alpine $DOCKER_REPO_SLUG:3.8-alpine-amd64 $DOCKER_REPO_SLUG:3.8-alpine-arm32v7"
                sh "docker manifest push $DOCKER_REPO_SLUG:3.8-alpine"
                // latest
                sh "docker manifest create $DOCKER_REPO_SLUG:latest $DOCKER_REPO_SLUG:3.8-alpine-amd64 $DOCKER_REPO_SLUG:3.8-alpine-arm32v7"
                sh "docker manifest push $DOCKER_REPO_SLUG:latest"
            }
        }
    }
}
