import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const TimerButton = ({ onPress, isCounting }) => {
  const buttonText = isCounting ? "J'ai reçu mon café" : "J'arrive à la machine à café";

  return (
    <TouchableOpacity onPress={onPress}>
      <View style={styles.container}>
        <View style={styles.box}>
          <Text style={styles.text}>{buttonText}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  box: {
    backgroundColor: 'orange',
    padding: 16,
    borderRadius: 8,
  },
  text: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default TimerButton;
