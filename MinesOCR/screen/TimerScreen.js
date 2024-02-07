import React, { useState, useEffect, useRef } from "react";
import { StyleSheet, View, Text } from "react-native";
import TimerButton from "../assets/TimerButton";
import TwoBlackBoxes from "../assets/BlackBoxes";
import Header from "../assets/Header";
import Footer from "../assets/Footer";
import NavigationButton from "../assets/ChangeScreenButton";
import { Client } from "paho-mqtt";

const TimerPage = ({ navigation }) => {
  const [leftValue, setLeftValue] = useState(0);
  const [rightValue, setRightValue] = useState(0);
  const [isCounting, setisCounting] = useState(false);
  const latestMessage = useRef(null);

  useEffect(() => {
    const client = new Client("ws://broker.emqx.io:8083/mqtt", "clientId");

    function onConnect() {
      console.log("Connected to MQTT broker");
      client.subscribe("CoffeeRush/AddWaitingTime");
      console.log("Subscribed to topic AddWaitingTime");
    }

    function onMessageArrived(message) {
      latestMessage.current = message.payloadString;
      console.log("Received message:", latestMessage.current);
    }

    client.onMessageArrived = onMessageArrived;
    client.connect({
      onSuccess: onConnect,
    });

    return () => {
      client.disconnect();
    };
  }, []);

  useEffect(() => {
    let interval;

    if (isCounting) {
      interval = setInterval(() => {
        if (rightValue === 59) {
          setRightValue(0);
          setLeftValue((prevLeftValue) => prevLeftValue + 1);
        } else {
          setRightValue((prevRightValue) => prevRightValue + 1);
        }
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [isCounting, rightValue]);

  const handleButtonPress = () => {
    if (isCounting ) {
      
      const client = new Client("ws://broker.emqx.io:8083/mqtt", "clientId");

      function onConnect() {
        let seconds = leftValue*60+rightValue;
        console.log("Connected to MQTT broker");
        client.publish("CoffeeRush/AddWaitingTime", seconds.toString());
        console.log("Published left and right values");
        setLeftValue(0);
        setRightValue(0);

      }

      client.connect({
        onSuccess: onConnect,
      });
    }
    
    setisCounting((previsCounting) => !previsCounting);
  };

  return (
    <View style={styles.container}>
      <Header text="Coffee Rush" />
      <Text style={styles.text}>Aidez-nous à améliorer notre application !</Text>
      <TwoBlackBoxes
        leftValue={leftValue}
        rightValue={rightValue.toString().padStart(2, "0")}
      />
      <View style={styles.buttonContainer}>
        <TimerButton onPress={handleButtonPress} isCounting={isCounting} />
      </View>
      <NavigationButton navigation={navigation} destination="Home" title="Retour à l'accueil" />
      <Footer text="Copyright © 2023 Techlab"/>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection:'column',
    backgroundColor: "white",
    justifyContent: "center",
    alignItems: "center",
    },
    text:{
    fontSize: 20,
    textAlign: "center",
    marginTop:40,
    marginBottom:40,
    },
    buttonContainer: {
    marginTop: 60,
    },
    });
    
    export default TimerPage;
