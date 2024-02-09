import React, { useState, useEffect, useRef } from "react";
import { StyleSheet, View, Text } from "react-native";
import TimerButton from "../assets/TimerButton";
import TwoBlackBoxes from "../assets/BlackBoxes";
import Header from "../assets/Header";
import Footer from "../assets/Footer";
import { Client } from "paho-mqtt";
import NavigationButton1 from "../assets/ChangeScreenButton1";

const TimerPage = ({ navigation }) => {
  const [leftValue, setLeftValue] = useState(0);
  const [rightValue, setRightValue] = useState(0);
  const [isCounting, setisCounting] = useState(false);
  const [predictedText, setPredictedText] = useState("");
  const latestMessage = useRef(null);

  useEffect(() => {
    const client = new Client("ws://broker.emqx.io:8083/mqtt", "clientId");

    function onConnect() {
      console.log("Connected to MQTT broker");
      client.subscribe("MinesOCR/Prediction");
      console.log("Subscribed to topic Prediction");
    }

    function onMessageArrived(message) {
      latestMessage.current = message.payloadString;
      console.log("Received message:", latestMessage.current);
      setPredictedText(latestMessage.current);
    }

    client.onMessageArrived = onMessageArrived;
    client.connect({
      onSuccess: onConnect,
    });

    return () => {
      client.disconnect();
    };
  }, []);

  return (
    <View style={styles.container}>
      <Header text="Optic2Mines" />
      <Text style={styles.text}>Qu'est-ce que c'est écrit sur le tableau?</Text>
      <Text style={styles.text}>{predictedText}</Text>
      <NavigationButton1
        navigation={navigation}
        destination="Optic"
        title="Retour à l'accueil"
      />
      <Footer text="Copyright © 2024 Techlab" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
    backgroundColor: "white",
    justifyContent: "center",
    alignItems: "center",
  },
  text: {
    fontSize: 20,
    textAlign: "center",
    marginTop: 40,
    marginBottom: 40,
  },
  buttonContainer: {
    marginTop: 60,
  },
});

export default TimerPage;
