import React from "react";
import { StyleSheet, View, Text } from "react-native";
import { Image } from "react-native";
import { ImageBackground } from "react-native";

const BlackBox = ({ value }) => {
  return (
    <View style={styles.box}>
      <Text style={styles.value}>{value}</Text>
    </View>
  );
};

const ImageBox = ({ value }) => {
  return (
    <View style={styles.box}>
      <Image
        source={require("../assets/iciNancy.jpg")}
        style={{ width: 100 }}
      />
    </View>
  );
};

const LBoxAndText = ({ leftValue, rightValue }) => {
  return (
    <View style={styles.container}>
      <ImageBox value={leftValue} />
      <Text style={styles.colon}>:</Text>
      <BlackBox value={rightValue} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 40,
    borderRadius: 10,
  },
  box: {
    width: 150,
    height: 150,
    backgroundColor: "black",
    borderRadius: 10,
    margin: 5,
    marginTop: 0,
    justifyContent: "center",
    alignItems: "center",
  },
  value: {
    color: "white",
    fontSize: 96,
    fontWeight: "bold",
  },
  colon: {
    color: "black",
    fontSize: 96,
    alignSelf: "center",
  },
});

export default LBoxAndText;
