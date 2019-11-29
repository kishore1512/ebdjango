pipeline{
   agent any 

   stages {
    stage ("Init") {
          steps {
          sh 'eb init django-demo -p python-3.6 --region us-east-1 -k Test-teej'
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
