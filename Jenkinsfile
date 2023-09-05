pipeline {
  agent any
  
  stages { 
     stage('Build docker image') {
        steps {  
            sh ' docker build -t pythonapp:$BUILD_NUMBER .'
        }
     }
     stage("run docker container"){
        steps{
                sh "docker run -d --name python -p 8090:8090 pythonapp:$BUILD_NUMBER"
        }
     }
  }   

}  
