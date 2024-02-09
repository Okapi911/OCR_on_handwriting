import React from "react";
import { StyleSheet, View, Text } from "react-native";
import { Image } from "react-native";
import { ImageBackground } from "react-native";

const BlackBox = ({ value }) => {
  return (
    <View style={styles.box2}>
      <Text style={styles.value}>The dumb Unitree from somewhere in China</Text>
    </View>
  );
};

const ImageBox = ({ value }) => {
  return (
    <View style={styles.box}>
      <Image
        source={require("../assets/unitree.jpg")}
        style={{ width: 150, height: 150, borderRadius: 10 }}
      />
    </View>
  );
};

const RBoxAndText = ({ leftValue, rightValue }) => {
  return (
    <View style={styles.container}>
      <BlackBox value={leftValue} />
      <ImageBox value={rightValue} />
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
  box2: {
    width: 150,
    height: 150,
    backgroundColor: "transparent",
    borderRadius: 10,
    margin: 5,
    marginTop: 0,
    justifyContent: "center",
    alignItems: "center",
    color: "black",
  },

  value: {
    color: "#696969" /** Super cool custom color */,
    fontSize: 20,
    fontWeight: "500",
    textAlign: "center",
  },
  colon: {
    color: "black",
    fontSize: 96,
    alignSelf: "center",
  },
});

export default RBoxAndText;
