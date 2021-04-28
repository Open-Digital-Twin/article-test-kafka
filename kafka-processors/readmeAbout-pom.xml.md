most of the times it wont work without this:

         <dependency> 
	         <groupId>org.slf4j</groupId> 
	         <artifactId>slf4j-simple</artifactId> 
	         <version>1.7.9</version> 
         </dependency>

You will want to build the projects with

	mvn clean compile assembly:single
	
This will add all de dependecies inside the jar file, otherwise kafka may and will complain about their abscence 

Use this plugin for ease of use 

            <!-- Plugin to building a jar with dependencies, without worring about versioning and stuff -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
     		    <artifactId>maven-assembly-plugin</artifactId>
    			<version>3.1.0</version>  
    	        <configuration>
    		        <appendAssemblyId>false</appendAssemblyId>
    		        <archive>
       			        <manifest>
      			            <mainClass>fully.qualified.MainClass</mainClass>
     			        </manifest>
    			    </archive>
     			    <descriptorRefs>
    			        <descriptorRef>jar-with-dependencies</descriptorRef>
    			    </descriptorRefs>
    			</configuration>
 		    </plugin>
