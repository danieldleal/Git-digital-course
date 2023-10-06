using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System;
using System.Collections.Generic;
using System.Windows;

namespace Test
{

    /// <summary>
    /// Interaction logic for Panel.xaml
    /// </summary>
    public partial class Panel : Window

    {
        //Get UIDocument and Document - Global variables
        UIDocument uidoc;
        Document Doc;

        public Panel(Document doc)
        {
            InitializeComponent();
            Doc = doc;
        }

        public void Set_RoomFinishes(object sender, RoutedEventArgs e)
        {
            //Function that retrieve all Rooms in the project to the ComboBox as soon as the application button is activated in the panel
            IList<Element> allRooms = new FilteredElementCollector(Doc)
            .OfCategory(BuiltInCategory.OST_Rooms).ToElements();
            try
            {
                foreach (Element room in allRooms)
                {
                    available_rooms.Items.Add(room);
                }
            }
            catch (Exception)
            {
                TaskDialog.Show("Error", "Try again");
            }
        }

        private void ApplyButton_Click(object sender, RoutedEventArgs e)
        {
            IList<Element> allRooms = new FilteredElementCollector(Doc)
            .OfCategory(BuiltInCategory.OST_Rooms).ToElements();

            string selectedRoom = this.available_rooms.SelectedItem.ToString();
            Element roomElement = null;

            if (UpperLimit == "" || LimitOffset == "" || BaseOffset == "" || Department == "" || BaseFinish == "" || CeilingFinish == "" || WallFinish == "" || FloorFinish == "")
            {
                TaskDialog.Show("Null", string.Format("Please fill out all the fields"));
            }
            else
            {
                foreach (Element room in allRooms)
                {
                    roomElement = room;
                    IList<Parameter> roomFin = roomElement.GetOrderedParameters();

                    //Set Parameters Values
                    using (Transaction setFinishes = new Transaction(Doc, "Set Room Finishes"))
                    {
                        setFinishes.Start();

                        Parameter UpperLimit = roomElement.get_Parameter(BuiltInParameter.ROOM_UPPER_LEVEL);
                        Parameter LimitOffset = roomElement.get_Parameter(BuiltInParameter.ROOM_UPPER_OFFSET);
                        Parameter BaseOffset = roomElement.get_Parameter(BuiltInParameter.ROOM_LOWER_OFFSET);
                        Parameter Department = roomElement.get_Parameter(BuiltInParameter.ROOM_DEPARTMENT);
                        Parameter BaseFinish = roomElement.get_Parameter(BuiltInParameter.ROOM_FINISH_BASE);
                        Parameter CeilingFinish = roomElement.get_Parameter(BuiltInParameter.ROOM_FINISH_CEILING);
                        Parameter WallFinish = roomElement.get_Parameter(BuiltInParameter.ROOM_FINISH_WALL);
                        Parameter FloorFinish = roomElement.get_Parameter(BuiltInParameter.ROOM_FINISH_FLOOR);
                        

                        setFinishes.Commit();
                        Close();


                        TaskDialog.Show("Parameter Values", string.Format("Room: {0} \n Department: {1} \n Base Finish: {2} \n Ceiling Finish: {3} \n Wall Finish: {4} \n Floor Finish: {5} ",
                        roomElement.Name, Department.SetValueString(""), BaseFinish.SetValueString(""),
                        CeilingFinish.SetValueString(""), WallFinish.SetValueString(""), FloorFinish.SetValueString("")));

                    }
                }
            }
        }
        public string UpperLimit
        {
            get { return this.SetRC_UpperLimit.Name; }
        }

        public string LimitOffset
        {
            get { return this.SetRC_LimitOffset.Name; }
        }

        public string BaseOffset
        {
            get { return this.SetRC_BaseOffset.Name; }
        }

        public string Department
        {
            get { return this.SetRF_Department.Name; }
        }

        public string BaseFinish
        {
            get { return this.SetRF_BaseFinish.Name; }
        }

        public string CeilingFinish
        {
            get { return this.SetRF_CeilingFinish.Name; }
        }

        public string WallFinish
        {
            get { return this.SetRF_WallFinish.Name; }
        }

        public string FloorFinish
        {
            get { return this.SetRF_FloorFinish.Name; }
        }
    }
}