pipeline {
  agent {label 'Built-In Node'}
  
  stages { 
     stage('Build docker image') {
        steps {  
            sh ' docker build -t pythonapp:$BUILD_NUMBER .'
        }
     }
     stage("run docker container"){
        steps{
                sh "docker run -d --name python -p 8070:8070 pythonapp:$BUILD_NUMBER"
        }
     }
  }   

}  
