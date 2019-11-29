pipeline{
   agent any 

   stages {
    stage ("Init") {
          steps {
          sh 'eb init -p python-3.6 django-demo --region us-east-1 -k Test-teejadding r'
          }          
         }
    stage ("Use env") {
          steps {
          sh 'eb use django-demo-env'
          }         
         }
    stage ("Deploy") {
          steps {
          sh 'eb deploy --staged'                   
         }
    }

   }
}
