import React from "react";
import { TouchableOpacity, Text, StyleSheet } from "react-native";

const Button = ({ onPress }) => {
  return (
    <TouchableOpacity style={styles.button} onPress={onPress}>
      <Text style={styles.text}>Follow the lesson in App</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    backgroundColor: "#063304",
    padding: 10,
    borderRadius: 5,
    alignItems: "center",
    marginTop: 20,
    marginBottom: 10,
  },
  text: {
    color: "white",
    fontWeight: "bold",
    fontSize: 20,
  },
});

export default Button;
