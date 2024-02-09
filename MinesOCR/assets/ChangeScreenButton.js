import React from "react";
import { Button, StyleSheet, View } from "react-native";

const NavigationButton = ({ navigation, destination, title }) => {
  const onPress = () => {
    navigation.navigate(destination);
  };

  return (
    <View style={styles.container}>
      <Button
        title="Follow the lesson in App"
        onPress={onPress}
        color="#b40c00"
        text-color="black"
        fontSize="20"
      ></Button>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
    margin: 10,
    borderRadius: 20,
  },
});

export default NavigationButton;
