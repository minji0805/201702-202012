import React from 'react';
import { RenderAfterNavermapsLoaded, NaverMap,Marker} from 'react-naver-maps'; 

function NaverMapAPI() {
  const navermaps = window.naver.maps;
  return (
    <NaverMap
      mapDivId={'maps-getting-started-uncontrolled'}
      style={{
        width: '100%',
        height: '85vh' 
      }}
      defaultCenter={{ lat: 36.629281, lng: 127.456328}}
      defaultZoom={13}
      >
      <Marker
        key={1}
        position={new navermaps.LatLng(36.629281, 127.456328)}
        animation={2}
        onClick={() => {alert('충북대학교');}}
      />
    </NaverMap>
  );
}

function App() {
  return (
    <RenderAfterNavermapsLoaded
      ncpClientId={'z2j2msac1o'}
      error={<p>Maps Load Error</p>}
      loading={<p>Maps Loading...</p>}
    >
      <NaverMapAPI />
    </RenderAfterNavermapsLoaded>
  );
}

export default App;