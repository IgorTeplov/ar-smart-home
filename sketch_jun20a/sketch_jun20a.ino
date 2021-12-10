#define in1 8
#define in2 9
#define in3 10
#define in4 11
#define analogLightDetector A1

#define userFlag 13

#define d360 510

int dl = 2;

int max_steeps = 1;

void setup() {
    Serial.begin(9600);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);
    pinMode(userFlag, OUTPUT);

    pinMode(analogLightDetector, INPUT);
}

void run_left(int steeps){ // open
  for(int count = 0; count < steeps; count++){
    digitalWrite(in1, HIGH); 
    digitalWrite(in2, LOW); 
    digitalWrite(in3, LOW); 
    digitalWrite(in4, HIGH);
    delay(dl);

    digitalWrite(in1, HIGH); 
    digitalWrite(in2, HIGH); 
    digitalWrite(in3, LOW); 
    digitalWrite(in4, LOW);
    delay(dl);

    digitalWrite(in1, LOW); 
    digitalWrite(in2, HIGH); 
    digitalWrite(in3, HIGH); 
    digitalWrite(in4, LOW);
    delay(dl);

    digitalWrite(in1, LOW); 
    digitalWrite(in2, LOW); 
    digitalWrite(in3, HIGH); 
    digitalWrite(in4, HIGH);
    delay(dl);
  }
}

void run_right(int steeps){ // close
  for(int count = 0; count < steeps; count++){
    digitalWrite(in1, LOW); 
    digitalWrite(in2, LOW); 
    digitalWrite(in3, HIGH); 
    digitalWrite(in4, HIGH);
    delay(dl);
    
    digitalWrite(in1, LOW); 
    digitalWrite(in2, HIGH); 
    digitalWrite(in3, HIGH); 
    digitalWrite(in4, LOW);
    delay(dl);
    
    digitalWrite(in1, HIGH); 
    digitalWrite(in2, HIGH); 
    digitalWrite(in3, LOW); 
    digitalWrite(in4, LOW);
    delay(dl);
    
    digitalWrite(in1, HIGH); 
    digitalWrite(in2, LOW); 
    digitalWrite(in3, LOW); 
    digitalWrite(in4, HIGH);
    delay(dl);
  }
}


char buffer = '0';
int rot = 0;

int open_w = 0;
int max_open_w = 1000;
int min_open_w = 0;

int open_hight_value = 1000;

bool user_control = false;

void loop() {
  int light = analogRead(analogLightDetector);
  
  if (Serial.available() > 0) {
    byte a = Serial.read();
    Serial.println(a);
    
    if(a == 130){
      rot = 1;
    }
    else if(a == 140){
      rot = -1;
    }
    else if(a == 142){
      user_control = !user_control;
    }
    else if(a == 252){
      rot = rot;
    }
  }
  digitalWrite(userFlag, LOW); 
  if(user_control){
    digitalWrite(userFlag, HIGH); 
    if (rot == 1){
      while(open_w < max_open_w){
        run_left(1);
        open_w++;
      }
    }else if(rot == -1){
      while(min_open_w < open_w){
        run_right(1);
        open_w--;
      }    
    }
  }else{
    if (light > open_hight_value){
      while(open_w < max_open_w){
        run_left(1);
        open_w++;
      }
    }else if(light <= open_hight_value){
      while(min_open_w < open_w){
        run_right(1);
        open_w--;
      }    
    }

  }
  
}
