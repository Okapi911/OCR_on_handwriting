import React from "react";
import { View, Text, StyleSheet } from "react-native";

const PersonBox = ({ nbPeople }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>OCR with robots on Whiteboard Handwriting</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: "green",
    padding: 20,
    borderRadius: 10,
    marginTop: 5,
  },
  text: {
    color: "white",
    fontWeight: "bold",
    fontSize: 22,
    textAlign: "center",
  },
});

export default PersonBox;
