import React, { Component } from 'react'; 
import { View , StatusBar} from 'react-native'; 
import styles from '../styles'; 
import Camera from 'react-native-camera';

export default class Application extends Component { 
    constructor(props) { 
        super(); 
        this.camera = null;
    } 

    render() { 
        return ( 
        <View style={styles.container}>
             <StatusBar animated hidden />
             <Camera
               ref={(cam)=> {
                   this.camera = cam;
               }}
               style={styles.preview}
             />
        </View>
              );
    }
}

