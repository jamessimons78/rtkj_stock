//+------------------------------------------------------------------+
//|                                                      QZM_ATR.mq4 |
//|                                                    Qingzhao Ming |
//|                                      https://www.FinRobot.com.cn |
//|           记录指定品种当前波动幅度到文件中，提交给“交易助手”使用 |
//+------------------------------------------------------------------+
#property copyright "Qingzhao Ming"
#property link      "https://www.FinRobot.com.cn"
#property version   "1.01"
#property strict

string inp_Symbol_1 = "EURUSD";     //监控的第1个品种
string inp_Symbol_2 = "GBPUSD";     //监控的第2个品种
string inp_Symbol_3 = "XAUUSD";     //监控的第3个品种
string inp_Symbol_4 = "USDJPY";     //监控的第4个品种
int inp_ATR_Period = 20;            //与过去N日的ATR相比
int inp_nSeconds = 5;               //数据刷新间隔的秒数

double pre_ATR_1, pre_ATR_2, pre_ATR_3, pre_ATR_4;
int n_USD;
string Symbol_1, Symbol_2, Symbol_3, Symbol_4;
string write_txt;
datetime pre_Time;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   // 取直盘货币对除美元的另一个货币
   n_USD = StringFind(inp_Symbol_1, "USD", 0);
   if(n_USD==0) Symbol_1 = StringSubstr(inp_Symbol_1, 3, 3);
   else if(n_USD==3) Symbol_1 = StringSubstr(inp_Symbol_1, 0, 3);

   n_USD = StringFind(inp_Symbol_2, "USD", 0);
   if(n_USD==0) Symbol_2 = StringSubstr(inp_Symbol_2, 3, 3);
   else if(n_USD==3) Symbol_2 = StringSubstr(inp_Symbol_2, 0, 3);

   n_USD = StringFind(inp_Symbol_3, "USD", 0);
   if(n_USD==0) Symbol_3 = StringSubstr(inp_Symbol_3, 3, 3);
   else if(n_USD==3) Symbol_3 = StringSubstr(inp_Symbol_3, 0, 3);

   n_USD = StringFind(inp_Symbol_4, "USD", 0);
   if(n_USD==0) Symbol_4 = StringSubstr(inp_Symbol_4, 3, 3);
   else if(n_USD==3) Symbol_4 = StringSubstr(inp_Symbol_4, 0, 3);
   
   pre_Time = TimeLocal();

   return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
}
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   // 每隔几秒钟就计算一次
   if(TimeLocal() - pre_Time >= inp_nSeconds)
   {
      myReadData();

      // 对前三个品种的ATR进行倒序排列，波动大的放在前面，没有重点考虑交易第四个品种USDJPY
      double x_array[3] = {0, 0, 0};
      x_array[0] = pre_ATR_1;
      x_array[1] = pre_ATR_2;
      x_array[2] = pre_ATR_3;
      ArraySort(x_array, 3, 0, MODE_DESCEND);
     
      write_txt = "";
      if(x_array[0]==pre_ATR_1) write_txt += Symbol_1 + ":" + DoubleToStr(pre_ATR_1, 2) + ", ";
      else if(x_array[0]==pre_ATR_2) write_txt += Symbol_2 + ":" + DoubleToStr(pre_ATR_2, 2) + ", ";
      else write_txt += Symbol_3 + ":" + DoubleToStr(pre_ATR_3, 2) + ", ";

      if(x_array[1]==pre_ATR_1) write_txt += Symbol_1 + ":" + DoubleToStr(pre_ATR_1, 2) + ", ";
      else if(x_array[1]==pre_ATR_2) write_txt += Symbol_2 + ":" + DoubleToStr(pre_ATR_2, 2) + ", ";
      else write_txt += Symbol_3 + ":" + DoubleToStr(pre_ATR_3, 2) + ", ";

      if(x_array[2]==pre_ATR_1) write_txt += Symbol_1 + ":" + DoubleToStr(pre_ATR_1, 2) + ", ";
      else if(x_array[2]==pre_ATR_2) write_txt += Symbol_2 + ":" + DoubleToStr(pre_ATR_2, 2) + ", ";
      else write_txt += Symbol_3 + ":" + DoubleToStr(pre_ATR_3, 2) + ", ";

      write_txt += Symbol_4 + ":" + DoubleToStr(pre_ATR_4, 2) + "; " + TimeToStr(TimeLocal(),TIME_SECONDS);
      // printf(write_txt);
     
      // 将监控的ATR数据写入文件中，供“交易助手”读取
      string file_name = "myatr.txt";
      int handle_write = FileOpen(file_name, FILE_TXT|FILE_WRITE);
      if(handle_write!=INVALID_HANDLE)
      {
         FileWrite(handle_write, write_txt);
         FileClose(handle_write); 
      }
     
      pre_Time = TimeLocal();
   }
}
//+------------------------------------------------------------------+
void myReadData()
{
   double ATR_1, ATR_2, ATR_3, ATR_4, H_1, H_2, H_3, H_4, L_1, L_2, L_3, L_4, C_1, C_2, C_3, C_4;
   
   ATR_1 = iATR(inp_Symbol_1, PERIOD_D1, inp_ATR_Period, 1);
   ATR_2 = iATR(inp_Symbol_2, PERIOD_D1, inp_ATR_Period, 1);
   ATR_3 = iATR(inp_Symbol_3, PERIOD_D1, inp_ATR_Period, 1);
   ATR_4 = iATR(inp_Symbol_4, PERIOD_D1, inp_ATR_Period, 1);
   H_1 = iHigh(inp_Symbol_1, PERIOD_D1, 0);
   L_1 = iLow(inp_Symbol_1, PERIOD_D1, 0);
   H_2 = iHigh(inp_Symbol_2, PERIOD_D1, 0);
   L_2 = iLow(inp_Symbol_2, PERIOD_D1, 0);
   H_3 = iHigh(inp_Symbol_3, PERIOD_D1, 0);
   L_3 = iLow(inp_Symbol_3, PERIOD_D1, 0);
   H_4 = iHigh(inp_Symbol_4, PERIOD_D1, 0);
   L_4 = iLow(inp_Symbol_4, PERIOD_D1, 0);
   C_1 = iClose(inp_Symbol_1, PERIOD_CURRENT, 0);
   C_2 = iClose(inp_Symbol_2, PERIOD_CURRENT, 0);
   C_3 = iClose(inp_Symbol_3, PERIOD_CURRENT, 0);
   C_4 = iClose(inp_Symbol_4, PERIOD_CURRENT, 0);
   
   pre_ATR_1 = MathMax(H_1 - C_1, C_1 - L_1) / ATR_1;
   pre_ATR_2 = MathMax(H_2 - C_2, C_2 - L_2) / ATR_2;
   pre_ATR_3 = MathMax(H_3 - C_3, C_3 - L_3) / ATR_3;
   pre_ATR_4 = MathMax(H_4 - C_4, C_4 - L_4) / ATR_4;
}