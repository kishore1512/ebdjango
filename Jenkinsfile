pipeline{
   agent any 

   stages {
    stage ("Init") {
          steps {
          sh 'eb init django-demo'
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
