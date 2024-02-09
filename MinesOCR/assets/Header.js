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
    backgroundColor: "transparent",
    height: 150,
    justifyContent: "center",
    alignItems: "center",
  },
  text: {
    fontSize: 30,
    fontWeight: "bold",
  },
});

export default Header;
