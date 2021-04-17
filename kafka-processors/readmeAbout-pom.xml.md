most of the times it wont work without this:

         <dependency> 
	         <groupId>org.slf4j</groupId> 
	         <artifactId>slf4j-simple</artifactId> 
	         <version>1.7.9</version> 
         </dependency>

You will want to build the projects with

	mvn clean compile assembly:single
	
This will add all de dependecies inside the jar file, otherwise kafka may and will complain about their abscence 
