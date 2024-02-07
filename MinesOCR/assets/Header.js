import React from "react";
import { StyleSheet, View, Text } from "react-native";

const Header = ({ text }) => {
  return (
    <View style={styles.header}>
      <Text style={styles.text}>{text}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    backgroundColor: "white",
    height: 80,
    justifyContent: "center",
    alignItems: "center",
  },
  text: {
    fontSize: 24,
    fontWeight: "bold",
  },
});

export default Header;
