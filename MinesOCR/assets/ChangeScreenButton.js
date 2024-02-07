import React from 'react';
import { Button, StyleSheet, View } from 'react-native';

const NavigationButton = ({ navigation, destination, title }) => {
  const onPress = () => {
    navigation.navigate(destination);
  };

  return (
    <View style={styles.container}>
      <Button title={title} onPress={onPress} color="#FFA500" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    margin: 10,
    borderRadius: 20,
  },
});

export default NavigationButton;
