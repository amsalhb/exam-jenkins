pipeline {
environment { // Declaration of environment variables
DOCKER_ID = "asmalhb" // replace this with your docker-id
DOCKER_IMAGE1 = "movie-service"
DOCKER_IMAGE2 = "cast-service"
DOCKER_TAG = "v.${BUILD_ID}.0" // we will tag our images with the current build in order to increment the value by 1 with each new build
}
agent any 
stages {
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

	stage('Docker run') {
            steps {
                script {
                    // Run container for movie-service
                    sh "docker run -d -p 8001:8000 --name movie-service ${DOCKER_ID}/${DOCKER_IMAGE1}:${DOCKER_TAG}"
                    
                    // Run container for cast-service
                    sh "docker run -d -p 8002:8000 --name cast-service ${DOCKER_ID}/${DOCKER_IMAGE2}:${DOCKER_TAG}"
                }
            }
        }
        
        stage('Test Acceptance') {
            steps {
                script {
                    // Test curl command to validate container response
                    sh "curl -sS localhost:8001/api/v1/movies"
                    sh "curl -sS localhost:8002/api/v1/casts"
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
        stage('Prepare Environment') {
            environment
            {
                KUBECONFIG = credentials("config") // we retrieve  kubeconfig from secret file called config saved on jenkins
            }
            steps {
                script {
                    // Crée le répertoire .kube et copie le fichier kubeconfig
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    '''
                }
            }
        }

        stage('Deploy Movie Service to Dev') {
            steps {
                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace dev
                    '''
                }
            }
        }

        stage('Deploy Cast Service to Dev') {
            steps {
                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace dev
                    '''
                }
            }
        }

        stage('Deploy dbs and nginx to Dev') {
            steps {
                script {
                    sh '''
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace dev
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace dev
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace dev
                    '''
                }
            }
        }
        
        stage('Deploy Movie Service to Staging') {
            steps {
                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace staging
                    '''
                }
            }
        }

	stage('Deploy Cast Service to Staging') {
            steps {
                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace staging
                    '''
                }
            }
        }

        stage('Deploy dbs and nginx to Staging') {
            steps {
                script {
                    sh '''
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace staging
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace staging
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace staging
                    '''
                }
            }
        }

        stage('Deploy Movie Service to QA') {
            steps {
                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy Cast Service to QA') {
            steps {
                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy dbs and nginx to QA') {
            steps {
                script {
                    sh '''
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace qa
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace qa
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy Movie Service to Prod') {
            timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }
            steps {
                dir('movie-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./movie-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install movie-service ./movie-service --values=values.yml --namespace prod
                    '''
                }
            }
        }

        stage('Deploy Cast Service to Prod') {
            timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }
            steps {
                dir('cast-service-rep') {
                    // Copie des valeurs et mise à jour du tag Docker
                    sh '''
                    cp ./cast-service/values.yaml values.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install cast-service ./cast-service --values=values.yml --namespace prod
                    '''
                }
            }
        }

        stage('Deploy dbs and nginx to Prod') {
            timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }
            steps {
                script {
                    sh '''
                    helm upgrade --install movie-db ./movie-db --values ./movie-db/values.yaml --namespace prod
                    helm upgrade --install cast-db ./cast-db --values ./cast-db/values.yaml --namespace prod
                    helm upgrade --install nginx ./nginx --values ./nginx/values.yaml --namespace prod
                    '''
                }
            }
        }

        
}
}