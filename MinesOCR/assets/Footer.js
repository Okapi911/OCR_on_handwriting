import React from "react";
import { View, Text, StyleSheet } from "react-native";

const Footer = ({ text }) => {
  return (
    <View style={styles.footer}>
      <Text style={styles.text}>{text}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  footer: {
    height: 60,
    backgroundColor: "transparent",
    alignItems: "center",
    justifyContent: "center",
    marginTop: "auto",
  },
  text: {
    fontSize: 16,
    color: "#000",
  },
});

export default Footer;
