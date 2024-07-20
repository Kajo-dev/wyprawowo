export class Welcome {
  constructor(welcomeHeader) {
    this.welcomeHeader = welcomeHeader;
  }

  getTimeOfDay = () => {
    const date = new Date();
    const hours = date.getHours();
    return {
      hours,
    };
  };

  tester = () => console.log("everything is fine!");
}