pipeline {
environment { // Declaration of environment variables
DOCKER_ID = "asmalhb" // replace this with your docker-id
DOCKER_IMAGE1 = "movie-service"
DOCKER_IMAGE2 = "cast-service"
DOCKER_TAG = "v.${BUILD_ID}.0" // we will tag our images with the current build in order to increment the value by 1 with each new build
}
agent any 
stages {
       stage('Deploy dbs to Dev') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    sh '''
	            rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace dev
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace dev
                    '''
                }
            }
        }

        stage('Deploy dbs to Staging') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace staging
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace staging
                    '''
                }
            }
        }

        stage('Deploy dbs to QA') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace qa
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy dbs to Prod') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace prod
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace prod
                    '''
                }
            }
        }
        stage(' Docker Build'){ // docker build image stage
            steps {
                script {
		// Build movie-service image
                sh '''
                 docker rm -f jenkins
                 docker build -t $DOCKER_ID/$DOCKER_IMAGE1:$DOCKER_TAG ./movie-service-rep
                sleep 6
                '''
		sh '''
                 docker build -t $DOCKER_ID/$DOCKER_IMAGE2:$DOCKER_TAG ./cast-service-rep
                sleep 6
                '''
                }
            }
        }
        
        stage('Docker Push') { //we pass the built images to our docker hub account
            environment
            {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS") // we retrieve  docker password from secret text called docker_hub_pass saved on jenkins
            }
            steps {

                script {
                sh '''
                docker login -u $DOCKER_ID -p $DOCKER_PASS
                docker push $DOCKER_ID/$DOCKER_IMAGE1:$DOCKER_TAG
		docker push $DOCKER_ID/$DOCKER_IMAGE2:$DOCKER_TAG
                '''
                }
            }

        }

        stage('Deploy Movie Service to Dev') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace dev
                    '''
                }
            }
        }

        stage('Deploy Cast Service to Dev') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace dev
                    '''
                }
            }
        }

        stage('Deploy nginx to Dev') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace dev
                    '''
                }
            }
        }
        
        stage('Deploy Movie Service to Staging') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace staging
                    '''
                }
            }
        }

	stage('Deploy Cast Service to Staging') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace staging
                    '''
                }
            }
        }

        stage('Deploy nginx to Staging') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace staging
                    '''
                }
            }
        }

        stage('Deploy Movie Service to QA') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy Cast Service to QA') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy nginx to QA') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy Movie Service to Prod') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
            // Create an Approval Button with a timeout of 15minutes.
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }

                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace prod
                    '''
                }
            }
        }

        stage('Deploy Cast Service to Prod') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
            // Create an Approval Button with a timeout of 15minutes.
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }

                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace prod
                    '''
                }
            }
        }

        stage('Deploy nginx to Prod') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
            // Create an Approval Button with a timeout of 15minutes.
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }

                script {
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    ls
                    cat $KUBECONFIG > .kube/config
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace prod
                    '''
                }
            }
        }

        
}
}
