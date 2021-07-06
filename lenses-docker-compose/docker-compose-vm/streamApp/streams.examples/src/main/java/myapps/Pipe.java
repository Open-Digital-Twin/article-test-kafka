package myapps;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.common.serialization.Serde;
// APACHE STREAMS IMPORTS
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.kstream.*;
//import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.kstream.Consumed;
// CONSUMER IMPORT
import org.apache.kafka.clients.consumer.ConsumerConfig;
// FASTER XML IMPORT
//import com.fasterxml.jackson.databind.JsonNode;
//import com.fasterxml.jackson.databind.ObjectMapper;
// CONFLUENT IMPORTS
//import io.confluent.examples.streams.avro.WikiFeed;
import io.confluent.kafka.serializers.AbstractKafkaAvroSerDeConfig;
//import io.confluent.kafka.streams.serdes.avro.GenericAvroSerde;
//import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
// JAVA IMPORTS
//import java.io.IOException;
import java.util.Properties;
import java.util.Arrays;
import java.util.Locale;
//import java.util.concurrent.CountDownLatch;
//import java.util.HashMap;
//import java.util.Map;
//import java.util.Collections;
import java.lang.Math;

// this needs mvn eclipse:eclipse so that eclipse can find the java stuff to auto complete
// BUILD THIS WITH ::  mvn clean compile assembly:single
public class Pipe {
    
	  static final String SOURCE_TOPIC = "mqtt";
	  static final String SINK_TOPIC = "mqttOut";

	  public static void main(final String[] args) {
	    final String bootstrapServers = args.length > 0 ? args[0] : "localhost:9094";
	    final String schemaRegistryUrl = args.length > 1 ? args[1] : "http://localhost:8081";
	    
	    final KafkaStreams streams = buildJsonToAvroStream(
	        bootstrapServers,
	        schemaRegistryUrl
	    );
	    
	    streams.start();
	    // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
	    Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
	  }
	
     static KafkaStreams buildJsonToAvroStream(final String bootstrapServers, final String schemaRegistryUrl) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pipe");
        props.put(StreamsConfig.CLIENT_ID_CONFIG, "streams-pipe-client");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
//        props.put(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, schemaRegistryUrl);
        // This is so you don't need to declare everytime which Serdes produces or consumes, but I declare anyways
        // since it makes easier to read after
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        
//        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, SpecificAvroSerde.class);
//        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
//        setting offset reset to earliest so that we can re-run the demo code with the same pre-loaded data
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

//        final ObjectMapper objectMapper = new ObjectMapper();
        StreamsBuilder builder = new StreamsBuilder();

        final KStream<String, String> source = builder.stream(SOURCE_TOPIC,
                Consumed.with(Serdes.String(), Serdes.String()));

        //---------------------------------------------------------------------------------------------------------------
        // Word count
        KStream<String, String> transformed = source;
        transformed.flatMapValues(value -> Arrays.asList(value.toLowerCase(Locale.getDefault()).split("\\W+")))
              .groupBy((key, value) -> value)
              .count(Materialized.<String, Long, KeyValueStore<Bytes, byte[]>>as("counts-store"))
              .toStream()
              .to(SINK_TOPIC, Produced.with(Serdes.String(), Serdes.Long()));
	            
	            
//	            transformed.to(SINK_TOPIC, Produced.valueSerde(Serdes.String()));

        //---------------------------------------------------------------------------------------------------------------
        // This is the logarithm processor, and  it works. It simply uses mapValues to get each value and apply the
        // log function from the Math library
//        	KStream<String, String> transformed = source.mapValues(
//        	    new ValueMapper<String, String>() {
//        	      @Override
//        	      public String apply(String value) {
//        	    	Double temp = Double.parseDouble(value);
//        	        // this is ugly but since kafka is extremely annoying to work with anything 
//        	    	// but strings, it will have to do (for now)
//        	    	Double logOf = Math.log(temp);
//        	    	String result = Double.toString(logOf);
//        	        
//        	    	return result;
//        	      }
//        	    });
         //---------------------------------------------------------------------------------------------------------------
        
        //You CAN make those functions as lambda, but then idk how to access inside the functions to apply the logic, so
        // i did not use lambda
        
        //--------------------------------------------------------------------------------------------------------------
        // This is the filter, it works and it filters if the number is higher than 50, if so it forwards the message to
        // the sink topic
//        KStream<String, String> filtro = source.filterNot(
//        	    new Predicate<String, String>() {
//        	      @Override
//        	      public boolean test(String key, String value) {
//        	    	float temp = Float.parseFloat(value);
//        	    	return temp <= 50;
//        	      }
//        	    });
        //--------------------------------------------------------------------------------------------------------------
        
//        
//        ClassCastException while producing data to topic mqttOut. A serializer 
//        (key: org.apache.kafka.common.serialization.ByteArraySerializer / 
//        		value: org.apache.kafka.common.serialization.ByteArraySerializer) 
//        is not compatible to the actual key or value type (key type: java.lang.String / 
//        		value type: java.lang.Integer). 
//        Change the default Serdes in StreamConfig or provide correct 
//        Serdes via method parameters (for example if using the DSL, 
//        		`#to(String topic, Produced<K, V> produced)` 
//        		with `Produced.keySerde(WindowedSerdes.timeWindowedSerdeFrom(String.class))`).

        
     //   source.to(SINK_TOPIC);

        return new KafkaStreams(builder.build(), props);
  
    }
}