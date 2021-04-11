package myapps;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;
import java.util.concurrent.CountDownLatch;

public class Pipe {
    
    public static void main(String[] args) throws Exception {
   
        // assuming that the Kafka broker this application is talking to runs on local machine with port 9092
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pipe");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");   

        //customize other configurations in the same map, for example, default serialization and deserialization libraries for the record key-value pairs:
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        


        //define the computational logic of our Streams application. In Kafka Streams this computational logic is defined as a topology of connected processor nodes. 
        //Use a topology builder to construct such a topology, 
        final StreamsBuilder builder = new StreamsBuilder();

        //And then create a source stream from a Kafka topic 
        KStream<String, String> source = builder.stream("mqtt");

        //Now we get a KStream that is continuously generating records from its source Kafka topic. 
        //The records are organized as String typed key-value pairs. 
        //The simplest thing we can do with this stream is to write it into another Kafka topic,
        source.to("mqttOut");



        //inspect what kind of topology is created from this builder by doing the following:
        final Topology topology = builder.build();
        final KafkaStreams streams = new KafkaStreams(topology, props);
        final CountDownLatch latch = new CountDownLatch(1);

        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
            }
        });

        try {
            streams.start();
            latch.await();
        } catch (Throwable e) {
            System.exit(1);
        }
        System.exit(0);
    }
}