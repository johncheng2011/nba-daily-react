import * as React from "react";
import { NavLink, withRouter } from "react-router-dom";
import "tabler-react/dist/Tabler.css";
import {
  Site,
  Nav,
  Grid,
  List,
  Button,
  RouterContextProvider,
} from "tabler-react";

import type { NotificationProps } from "tabler-react";

type Props = {|
  +children: React.Node,
|};

type State = {|
  notificationsObjects: Array<NotificationProps>,
|};

type subNavItem = {|
  +value: string,
  +to?: string,
  +icon?: string,
  +LinkComponent?: React.ElementType,
  +useExact?: boolean,
|};

type navItem = {|
  +value: string,
  +to?: string,
  +icon?: string,
  +active?: boolean,
  +LinkComponent?: React.ElementType,
  +subItems?: Array<subNavItem>,
  +useExact?: boolean,
|};

const navBarItems: Array<navItem> = [
  {
    value: "Home",
    to: "/",
    icon: "home",
    LinkComponent: withRouter(NavLink),
    useExact: true,
  },
 
  {
    value: "All Player's Stats",
    icon: "",
    to:"/all_players_pergame",
    LinkComponent: withRouter(NavLink),
    useExact:true,
   
  },
  {
    value: "All Player's ZScores",
    icon: "",
    to:"/all_players_zscores",
    LinkComponent: withRouter(NavLink),
    useExact: true,
  },
  
];



class SiteWrapper extends React.Component<Props, State> {


  render(): React.Node {

    return (
      <Site.Wrapper
        headerProps={{
          href: "/",
          alt: "NBA Daily",
          imageURL: "http://test-nba.herokuapp.com/logo192.png",
          navItems: (
            <Nav.Item type="div" className="d-none d-md-flex" style = {{paddingLeft:100}}>
          
                NBA Daily
    
            </Nav.Item>
          ),

        }}
        navProps={{ itemsObjects: navBarItems }}
        routerContextComponentType={withRouter(RouterContextProvider)}

      >
        {this.props.children}
        
      </Site.Wrapper>
    );
  }
}

export default SiteWrapper;